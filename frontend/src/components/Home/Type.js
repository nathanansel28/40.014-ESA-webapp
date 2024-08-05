import React from "react";
import Typewriter from "typewriter-effect";

function Type() {
  return (
    <Typewriter
      options={{
        strings: [
          "ALGORITHM RUNTIME",
          "MAKESPAN",
          "NUMBER OF TARDY JOBS",
          "WORK-IN-PROCESS (WIP) COSTS",
        ],
        autoStart: true,
        loop: true,
        deleteSpeed: 40,
      }}
    />
  );
}

export default Type;
