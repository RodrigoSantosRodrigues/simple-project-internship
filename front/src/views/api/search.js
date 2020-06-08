import axios from 'axios';

export {
  searchUser
};

async function searchUser() {
  return await axios.get('http://localhost:5000/v1/api/users/');
}
