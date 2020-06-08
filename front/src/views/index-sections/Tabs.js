import React from "react";
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';
import { makeStyles } from '@material-ui/core/styles';

// reactstrap components
import {
  Button, 
  Container,
  Row,
  Col
} from "reactstrap";

import { createUser } from '../api/register';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  margin: {
    margin: theme.spacing(1)
  },
  withoutLabel: {
    marginTop: theme.spacing(3),
  },
  textField: {
    width: '15ch',
  },
}));

function Tabs() {
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [nascimento, setNasc] = React.useState("");
  const [telefone, setTel] = React.useState("");
  var [userValue, setUserValue] = React.useState("user");
  var [passwordValue, setPasswordValue] = React.useState("");
  const classes = useStyles();
  console.log(setUserValue);

  return (
    <>
      <div className="section section-tabs" style={{ backgroundColor: '#5dbcd2' }}>
        <Container>
          <Row className="justify-content-md-center">
            <Col lg="6" md="12">
              <form className={classes.root} noValidate autoComplete="off">
                <div>
                  <div style= {{ color: 'white', paddingLeft: 130}}>
                    <h1>CADASTRO</h1>
                  </div>
                  <FormControl style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin} >
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Nome</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={name}
                      onChange={e => setName(e.target.value)}
                    />
                  </FormControl>
                  <FormControl  style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Email</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={email}
                      onChange={e => setEmail(e.target.value)}
                    />
                  </FormControl>
                  <FormControl style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Nascimento</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={nascimento}
                      onChange={e => setNasc(e.target.value)}
                    />
                  </FormControl>
                  <FormControl style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Telefone</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={telefone}
                      onChange={e => setTel(e.target.value)}
                    />
                  </FormControl>
                  <FormControl style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Senha</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={passwordValue}
                      onChange={e => setPasswordValue(e.target.value)}
                    />
                  </FormControl>
                </div>
                  <Button
                    className="btn-neutral btn-round"
                    color="info"
                    href="#pablo"
                    onClick={() =>
                      createUser(
                        name,
                        email,
                        passwordValue,
                        userValue,
                      )
                      .then(response => {
                        /*
                        if (response === false){
                          setAlertFailed(true);
                        }

                        if (response.status === 200){
                          setAlertSucess(true);
                          setNameValue("");
                          setLoginValue("");
                          setPasswordValue("");
                          setUserValue("");
                        }
                        */
                       console.log("Error")
                      })
                      .catch(console.error)}
                    size="lg"
                  >
                    CADASTRAR 
                  </Button>
              </form>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}

export default Tabs;
