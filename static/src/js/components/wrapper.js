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
      showCreationModal: false,
      movieFilterMessage: 'All movies:',
      genreFilter: '',
      actorFilter: ''
    };
    this.props.reduxStore.dispatch(fetchMovies(''));
  }

  onModalCancel = () => {
    this.setState({
      showCreationModal: false
    });
  };

  onModalSave = async data => {
    this.setState({
      showCreationModal: false
    });
    await this.props.reduxStore.dispatch(createMovie(data));
    await this.props.reduxStore.dispatch(fetchMovies(''));
    this.setState({
      movieFilterMessage: 'All movies ',
      genreFilter: '',
      actorFilter: ''
    });
  };

  showCreateModal = () => {
    this.setState({
      showCreationModal: true
    });
  };

  filterResults = () => {
    let params;
    if (
      this.state.genreFilter.trim() == '' &&
      this.state.actorFilter.trim() == ''
    ) {
      params = '';
      this.setState({
        movieFilterMessage: 'All movies:'
      });
    } else if (this.state.genreFilter.trim() == '') {
      //this is potentially bad due to no encoding
      params = '?actor=' + this.state.actorFilter;
      this.setState({
        movieFilterMessage: 'Movies with actor: ' + this.state.actorFilter
      });
    } else if (this.state.actorFilter.trim() == '') {
      params = '?genre=' + this.state.genreFilter;
      this.setState({
        movieFilterMessage: 'Movies with genre: ' + this.state.genreFilter
      });
    } else {
      params =
        '?genre=' + this.state.genreFilter + '&actor=' + this.state.actorFilter;
      this.setState({
        movieFilterMessage:
          'Movies with genre: ' +
          this.state.genreFilter +
          ' and actor: ' +
          this.state.actorFilter
      });
    }
    this.props.reduxStore.dispatch(fetchMovies(params));
  };

  updateGenreFilter = event => {
    this.setState({ genreFilter: event.target.value });
  };

  updateActorFilter = event => {
    this.setState({ actorFilter: event.target.value });
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
          <button className="control-button" onClick={this.showCreateModal}>
            create a new movie!
          </button>
          <button className="control-button" onClick={this.filterResults}>
            filter the results!
          </button>
          <div className="filter-box">
            <span className="filter-label"> by actor: </span>
            <input
              className="filter-input"
              type="text"
              onChange={this.updateActorFilter}
            />
          </div>
          <div className="filter-box">
            <span className="filter-label"> by genre: </span>
            <input
              className="filter-input"
              type="text"
              onChange={this.updateGenreFilter}
            />
          </div>
        </div>
        <div className="filter-message">{this.state.movieFilterMessage}</div>
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
