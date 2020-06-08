/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container, Row, Col } from "reactstrap";

function DarkFooter() {
  return (
    <footer style={{
      backgroundImage: "url(" + require("assets/img/imagens/rodape-desktop.jpg") + ")"
    }} className="footer" >
      <Container className="text-center">
        <Row className="justify-content-md-center">
          <Col lg="8" md="12">
            <h5 style={{ color: 'white'}} className="description">
              Fulano Beltrano de Oliveira
            </h5>
            <h5 style={{ color: 'white'}} className="description">
              FulanoBos@gmail.com
            </h5>
            <h5 style={{ color: 'white'}} className="description">
              (31) 9 9254888888
            </h5>
            <h5 style={{ color: 'white'}} className="description">
              Faculdade de Belo Horizonte
            </h5>
          </Col>
        </Row>
      </Container>
    </footer>
  );
}

export default DarkFooter;
