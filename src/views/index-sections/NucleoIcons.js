import React from "react";
// reactstrap components
import { Table, Container, Row, Col } from "reactstrap";

import { TableStyle } from './styles';

function NucleoIcons() {
  return (
    <>
      <div className="section section-nucleo-icons">
        <Container>
          <Row className="justify-content-md-center">
            <Col lg="8" md="10">
              <div style= {{ color: '#6ec6eb', paddingLeft: 100 }}>
                <h1 style={{ justifyContent:'center' }}>LISTA DE CADASTRO</h1>
              </div>
              <TableStyle style={{ paddingLeft: 30 }}>
                <table className="tg">
                  <tr>
                    <th style={{ width:80 }} className="tg-0lax"></th>
                    <th style={{ width:150 }} className="tg-c3ow">First Name</th>
                    <th style={{ width:150 }} className="tg-c3ow">Last Name</th>
                    <th style={{ width:150 }} className="tg-c3ow">Username</th>
                    <th style={{ width:150 }}>User</th>
                  </tr>
                  <tr>
                    <td className="tg-0pky">1</td>
                    <td className="tg-7jts">Mark</td>
                    <td className="tg-7jts">Otto</td>
                    <td className="tg-7jts">@mdo</td>
                    <td className="tg-7jts">@mdo</td>
                  </tr>
                  <tr>
                    <td className="tg-0pky">2</td>
                    <td className="tg-7jts">Jacob</td>
                    <td className="tg-7jts">Thornton</td>
                    <td className="tg-7jts">@fat</td>
                    <td className="tg-7jts">@mdo</td>
                  </tr>
                  <tr>
                    <td className="tg-0pky">3</td>
                    <td className="tg-7jts">Larry the Bird</td>
                    <td className="tg-7jts">@twitter</td>
                    <td className="tg-7jts">@fat</td>
                    <td className="tg-7jts">@mdo</td>
                  </tr>
                  <tr>
                    <td >3</td>
                    <td className="tg-7jts">Larry the Bird</td>
                    <td className="tg-7jts">@twitter</td>
                    <td className="tg-7jts">@fat</td>
                    <td className="tg-7jts">@mdo</td>
                  </tr>
                </table>
          
              </TableStyle>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}

export default NucleoIcons;
