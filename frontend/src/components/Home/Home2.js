import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import myImg from "../../Assets/inventory.svg";
import Tilt from "react-parallax-tilt";


function Home2() {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={8} className="home-about-description">
            <h1 style={{ fontSize: "2.6em" }}>
              ABOUT <span className="purple"> GANNT. </span> 
            </h1>
            <p className="home-about-body">
                Our web application is designed to help manufacturing companies optimize their assembly line scheduling.
                
              <br />
              <br />By incorporating <b className="purple"> heuristic methods</b>, we aim to create an intuitive and efficient tool that addresses the complexities of <b className="purple"> large-scale scheduling.</b>
              <br />
              <br />
              Our solution focuses on &nbsp;
              <i>
                <b className="purple">minimizing makespan, work in process, and inventory</b> 
                {" "},ultimately{" "}
                <b className="purple">
                    {" "}enhancing productivity and reducing operational inefficiencies.{" "}
                </b>
              </i>
              <br />
            </p>
          </Col>
          <Col md={4} className="myAvtar">
            <Tilt>
              <img src={myImg} className="img-fluid" alt="avatar" />
            </Tilt>
          </Col>
        </Row>
        
      </Container>
    </Container>
  );
}
export default Home2;
