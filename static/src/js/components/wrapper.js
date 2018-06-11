import React from 'react';
import '../../css/wrapper.css';
import MovieBox from '../components/movie-box';
import CreateMovieModal from '../components/create-movie-modal';
import PropTypes from 'prop-types';
import {
  incrementByTwo,
  replaceMovies,
  createMovie,
  fetchMovies
} from '../actions';

const pageData = global.pageData;

class Wrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showCreationModal: false
    };
    this.props.reduxStore.dispatch(fetchMovies());
  }

  onModalCancel = () => {
    this.setState({
      showCreationModal: false
    });
  };

  onModalSave = data => {
    this.setState({
      showCreationModal: false
    });
    // POST to create movie and also update the store
    this.props.reduxStore.dispatch(createMovie(data));
  };

  showModal = () => {
    this.setState({
      showCreationModal: true
    });
  };

  render() {
    const movies = this.props.reduxStore.getState().moviesToDisplay;
    if (this.props.reduxStore.getState().isLoading) {
      return <div className="loading-spinner" />;
    }

    if (this.state.showCreationModal) {
      return (
        <div>
          <CreateMovieModal
            onCancel={this.onModalCancel}
            onAdd={this.onModalSave}
          />
        </div>
      );
    }

    return (
      <div className="wrapper">
        <div>{this.props.reduxStore.getState().numberOfMovies}</div>
        <div className="controls-container">
          <button onClick={this.showModal}>create a new movie!</button>
        </div>
        <div className="movie-container">
          {movies.map(emp => <MovieBox name={emp.title} genre={emp.genre} />)}
        </div>
      </div>
    );
  }
}

Wrapper.propTypes = {
  reduxStore: PropTypes.object.isRequired
};

export default Wrapper;
