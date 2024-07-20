import React from "react";
import Typewriter from "typewriter-effect";

function Type() {
  return (
    <Typewriter
      options={{
        strings: [
          "INVENTORY",
          "MAKESPAN",
          "IDLE TIME/BOTTLENECKS",
          "NUMBER OF TARDY JOBS",
          "WORK-IN-PROCESS",
        ],
        autoStart: true,
        loop: true,
        deleteSpeed: 40,
      }}
    />
  );
}

export default Type;
