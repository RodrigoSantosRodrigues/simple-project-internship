import axios from "axios";

export { createUser };

async function createUser( name, email, password, user) {
  if (!!email && !!password) {
    //const base_url_user_service= process.env.REACT_APP_USER_SERVICE;
    try {
      const res= await axios.post('http://localhost:5000/v1/api/users/', 
                  {
                    "name": name,
                    "email": email,
                    "password": password,
                    "role": user,
                    "active": true,
                    "deleted_app": 0,
                    "created_app": 2,
                    "modified_app": 0
                  })
      return res;
    } catch (error) {
      return false;
    }
  } else {
    return false;
  }
}
