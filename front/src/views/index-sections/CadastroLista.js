import React from "react";
// reactstrap components
import { Container, Row, Col } from "reactstrap";

import { TableStyle } from './styles';

import { searchUser } from '../api/search';

function CadastroLista() {
  const [datas, setData] = React.useState([]);

  //Realizar chamada após cada cadastro, não colocar em produção.
  setTimeout(() => {
    searchUser()
      .then(response => {
        if (response.status === 200){
          setData(response.data);
        }
      })
      .catch(console.error)
  }, 3000);

  const cadastroStyle = {
    justifyContent:'center',
    color: '#6ec6eb', 
    paddingBottom: 30,
    fontSize: 20
  };

  return (
    <>
      <div className="section section-nucleo-icons">
        <Container>
          <Row style={{justifyContent: 'center'}} className="justify-content-md-center">
              <div style= {cadastroStyle}>
                <h3 className="h1-seo">LISTA DE CADASTRO</h3>
              </div>
            <Col lg="8" md="8" style={{paddingLeft: 30}}>
              <TableStyle >
                <table className="tg">
                  <tr>
                    <th style={{ width:80 }} className="tg-0lax"></th>
                    <th style={{ width:150 }} className="tg-c3ow">Name</th>
                    <th style={{ width:150 }} className="tg-c3ow">Email</th>
                    <th style={{ width:150 }} className="tg-c3ow">Nascimento</th>
                    <th style={{ width:150 }}>Telefone</th>
                  </tr>
                  {datas.map((value) => (
                            <tr>
                            <td className="tg-0pky">{value.id}</td>
                            <td className="tg-7jts">{value.name}</td>
                            <td className="tg-7jts">{value.email}</td>
                            <td className="tg-7jts">21/03/1992</td>
                            <td className="tg-7jts">(31) 955455555</td>
                          </tr>
                        ))}
                  <tr>
                    <td >15</td>
                    <td className="tg-7jts">Larry Kaply</td>
                    <td className="tg-7jts">kaply@gmail.com</td>
                    <td className="tg-7jts">03/08/1996</td>
                    <td className="tg-7jts">(31)95500000</td>
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

export default CadastroLista;
