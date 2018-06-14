import React from 'react';
import '../../css/create-movie-modal.css';

export default class CreateMovieModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      title: null,
      genre: null,
      actors: null
    };
  }

  updateTitle = event => {
    this.setState({ title: event.target.value });
  };

  updateGenre = event => {
    this.setState({ genre: event.target.value });
  };

  updateActors = event => {
    this.setState({ actors: event.target.value });
  };

  onSave = () => {
    if (!this.state.title || !this.state.genre) {
      this.setState({ error: 'title and genre are required!' });
      return;
    }
    let dat = {
      title: this.state.title.trim(),
      genre: this.state.genre.trim()
    };

    //this is fragile code, needs to be improved:
    if (this.state.actors) {
      let ar = this.state.actors.split(',');
      ar = ar.map(x => x.trim());
      dat['actors'] = ar;
    }
    this.props.onAdd(dat);
  };

  render() {
    return (
      <div className="create-movie-modal">
        this is the movie creation modal!
        {this.state.error && (
          <div className="error-message">error message: {this.state.error}</div>
        )}
        <div className="padding-around">
          <span className="input-label"> Title: </span>
          <input type="text" onChange={this.updateTitle} />
        </div>
        <div className="padding-around">
          <span className="input-label"> Genre: </span>
          <input type="text" onChange={this.updateGenre} />
        </div>
        <div className="padding-around">
          <span className="input-label">Actors (comma seperated):</span>
          <input
            className="large-textbox"
            type="text"
            onChange={this.updateActors}
          />
        </div>
        <div className="padding-around">
          <button onClick={this.onSave}>add the movie! </button>
          <button onClick={this.props.onCancel}>cancel</button>
        </div>
      </div>
    );
  }
}
