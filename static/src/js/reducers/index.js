const initialState = {
  isLoading: false,
  moviesToDisplay: []
};

export default (state = initialState, action) => {
  switch (action.type) {
    case 'REPLACE_MOVIES':
      return Object.assign({}, state, {
        moviesToDisplay: action.movies
      });

    case 'ADD_MOVIE':
      return Object.assign({}, state, {
        moviesToDisplay: [...state.moviesToDisplay, action.movie]
      });

    case 'START_REQUEST':
      return Object.assign({}, state, {
        isLoading: true
      });

    case 'END_REQUEST':
      return Object.assign({}, state, {
        isLoading: false
      });

    default:
      return state;
  }
};
