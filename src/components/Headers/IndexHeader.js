/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container } from "reactstrap";
// core components

function IndexHeader() {
  let pageHeader = React.createRef();

  React.useEffect(() => {
    if (window.innerWidth > 991) {
      const updateScroll = () => {
        let windowScrollTop = window.pageYOffset / 3;
        pageHeader.current.style.transform =
          "translate3d(0," + windowScrollTop + "px,0)";
      };
      window.addEventListener("scroll", updateScroll);
      return function cleanup() {
        window.removeEventListener("scroll", updateScroll);
      };
    }
  });

  return (
    <>
      <div className="page-header" filter-color="blue">
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/imagens/index-image.jpg") + ")"
          }}
          ref={pageHeader}
        ></div>
        <Container>
          <div style={{ textAlign: 'left'}} className="content-center brand">
            <h1 className="h1-seo">ESTÁGIO</h1>
            <h3>PROVA DE SELEÇÃO</h3>
          </div>
        </Container>
      </div>
    </>
  );
}

export default IndexHeader;
