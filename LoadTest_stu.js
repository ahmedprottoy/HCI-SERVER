import http from "k6/http";
import { check, sleep } from "k6";
import { SharedArray } from "k6/data";

// Define the number of virtual users
let numOfVUs = 40;

// Define the test duration
let testDuration = "1m";

// Generate unique student data
const students = new SharedArray("students", function () {
  let students = [];
  for (let i = 1; i <= numOfVUs; i++) {
    students.push({
      name: `Student ${__VU} ${i * 2}`,
      email: `test${__VU}_${i * 2}@gmail.com`, // Unique emails for each student
      gender: Math.random() > 0.5 ? "M" : "F",
      useGlass: Math.random() > 0.5,
      displayWidth: Math.floor(Math.random() * 100),
      displayHeight: Math.floor(Math.random() * 100),
      age: Math.floor(Math.random() * 100),
      education: "SWE",
      accuracy: Math.random() * 100,
    });
  }
  return students;
});

export let options = {
  stages: [
    { duration: testDuration, target: numOfVUs },
    { duration: "20s", target: 0 }, // Ramp down to observe final state
  ],
};

export default function () {
  let student = students[__VU - 1];

  let res = http.post(
    "http://localhost:8080/students",
    JSON.stringify(student),
    {
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );

  check(res, {
    "is status 200": (r) => r.status === 200,
  });

  sleep(1); // Pacing for realistic load
}
