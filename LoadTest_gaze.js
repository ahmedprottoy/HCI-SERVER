import http from "k6/http";
import { check, sleep } from "k6";
import { SharedArray } from "k6/data";

// Define the number of virtual users
let numOfVUs = 40;

// Define the test duration
let testDuration = "10m";

// Generate unique gaze info data
const gazeInfo = new SharedArray("gazeInfo", function () {
  let gazeInfoRecords = [];
  for (let i = 0; i < numOfVUs * 60; i++) {
    gazeInfoRecords.push({
      student_id: Math.floor(Math.random() * numOfVUs) + 1, // Random student id
      Timestamp: Math.floor(Date.now() / 1000).toString(), // Timestamp in specified format
      GazeX: Math.random() * 1000, // Adjust ranges as needed
      GazeY: Math.random() * 1000,
      GazeLeftx: Math.random() * 1000,
      GazeLefty: Math.random() * 1000,
      GazeRightx: Math.random() * 1000,
      GazeRighty: Math.random() * 1000,
      PupilLeft: Math.random() * 5,
      PupilRight: Math.random() * 5,
      FixationSeq: Math.random() * 10,
      SaccadeSeq: Math.random() * 5,
      Blink: Math.random() * 1,
      GazeAOI: Math.random() * 10,
      isMindWandered: Math.random() > 0.5,
      batchNo: __VU, // Unique batch number for each VU
    });
  }
  return gazeInfoRecords;
});

export let options = {
  vus: numOfVUs, // Set the number of virtual users
  duration: testDuration, // Set the test duration
};

export default function () {
  let gazeData = gazeInfo;

  let res = http.post("http://localhost:8080/gaze", JSON.stringify(gazeData), {
    headers: { "Content-Type": "application/json" },
  });

  check(res, {
    "is status 200": (r) => r.status === 200,
  });

  sleep(10); // Pacing
}
