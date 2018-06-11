import { postMovie, getMovies } from '../api';
// action creators below:

export function replaceMovies(movies) {
  return {
    type: 'REPLACE_MOVIES',
    movies
  };
}

export function beginRequest() {
  return {
    type: 'START_REQUEST'
  };
}

export function endRequest() {
  return {
    type: 'END_REQUEST'
  };
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function createMovie(data) {
  return async function(dispatch) {
    dispatch(beginRequest());
    const movie = await postMovie(data);
    await sleep(3000);
    dispatch(endRequest());
  };
}

export function fetchMovies(filters) {
  return async function(dispatch) {
    dispatch(beginRequest());
    const movies = await getMovies(filters);
    await sleep(2000);
    dispatch(replaceMovies(movies));
    dispatch(endRequest());
  };
}
