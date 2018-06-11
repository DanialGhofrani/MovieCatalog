import axios from 'axios';

export async function postMovie(data) {
  try {
    let result = await axios.post('http://localhost:5555/movie/', data);
    return result.data;
  } catch (e) {
    console.log('exception:', e);
    return null;
  }
}

export async function getMovies(data) {
  try {
    let result = await axios.get('http://localhost:5555/movie/');
    return result.data;
  } catch (e) {
    console.log('exception:', e);
    return null;
  }
}
