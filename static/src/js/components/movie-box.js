import React from 'react';
import '../../css/movie-box.css';

export default class MovieBox extends React.Component {
  render() {
    return (
      <div className="movie-box">
        <div>name: {this.props.name}</div>
        <div>genre: {this.props.genre}</div>
      </div>
    );
  }
}
