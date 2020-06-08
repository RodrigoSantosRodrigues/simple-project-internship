import React from "react";
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';
import { makeStyles } from '@material-ui/core/styles';

// reactstrap components
import {
  Container,
  Row,
  Col
} from "reactstrap";

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
  const [value, setValue] = React.useState("");
  const classes = useStyles();

  const handleChange = (value) =>{
    setValue(value);
  }

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
                      value={value}
                      onChange={e =>handleChange()}
                    />
                  </FormControl>
                  <FormControl  style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Email</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={value}
                      onChange={e =>handleChange()}
                    />
                  </FormControl>
                  <FormControl style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Nascimento</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={value}
                      onChange={e =>handleChange()}
                    />
                  </FormControl>
                  <FormControl style={{ borderBottom: '2px solid rgba(255, 255, 255, 0.42)' }} fullWidth className={classes.margin}>
                    <InputLabel style={{ color:'white'}} htmlFor="standard-adornment-amount">Telefone</InputLabel>
                    <Input
                      style={{ color:'white'}}
                      id="standard-adornment-amount"
                      value={value}
                      onChange={e =>handleChange()}
                    />
                  </FormControl>
                </div>
              </form>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}

export default Tabs;
