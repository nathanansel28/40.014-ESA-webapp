import React from "react";
import Typewriter from "typewriter-effect";

function Type() {
  return (
    <Typewriter
      options={{
        strings: [
          "LETSA",
          "SIMULATED ANNEALING",
          "EARLIEST DUE DATE",
          "LAGRANGIAN RELAXATION",
        ],
        autoStart: true,
        loop: true,
        deleteSpeed: 40,
      }}
    />
  );
}

export default Type;
