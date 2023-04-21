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


export async function apiPost(url, body_json) {
  try {
    console.log(`apiPost ${url}`);
    const response = await server.post(url, body_json);
    console.log('%c Sent:', 'color: green');
    console.log(body_json);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

