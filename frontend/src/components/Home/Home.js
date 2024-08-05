import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import manuLogo from "../../Assets/scheduler.svg";
import Particle from "../Particle";
import Home2 from "./Home2";
import Type from "./Type";

function Home() {
  return (
    <section>
      <Container fluid className="home-section" id="home">
        <Particle />
        <Container className="home-content">
          <Row>

            <Col md={5} style={{ paddingBottom: 20, paddingTop:30 }}>
                  <img
                    src={manuLogo}
                    alt="home pic"
                    className="img-fluid"
                    style={{ maxHeight: "400px" }}
                  />
              </Col>

            <Col md={7} className="home-header">

              <h1 className="heading-name">
                OPTIMISE <br></br>
                <strong className="main-name"> ASSEMBLY LINES </strong>
                <span className="wave" role="img" aria-labelledby="wave">
                  📦
                </span>
              </h1>

              <div style={{ padding: 50, textAlign: "left" }}>
                <Type />
              </div>
            </Col>

          </Row>
        </Container>
      </Container>
      <Home2 />
    </section>
  );
}

export default Home;
