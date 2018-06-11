import axios from 'axios';

//TODO: all of these URLs should be fetched from settings
export async function postMovie(data) {
  try {
    let result = await axios.post('http://localhost:5555/movie/', data);
    return result.data;
  } catch (e) {
    console.log('exception:', e);
    return null;
  }
}

export async function getMovies(filters) {
  try {
    const url = 'http://localhost:5555/movie/' + filters;
    let result = await axios.get(url);
    return result.data;
  } catch (e) {
    console.log('exception:', e);
    return null;
  }
}
