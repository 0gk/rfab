import axios from 'axios'


const server = axios.create({
        baseURL: 'http://fab.rlab.ru:9000',
        timeout: 10000,
    });


export async function apiGet(url) {
  try {
    console.log(`apiGet ${url}`);
    const response = await server.get(url);
    console.log('%c Received:', 'color: green');
    console.log(response);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};


/*
function displayMessage(message, type='info') {
//  this.$notify({ message: message, type: type});
  if (type === 'success') {
    console.log('%c' + message, 'color: green');
  } else if (type === 'error') {
    console.error(message);
  } else {
   console.log(message);
  };
};

*/
