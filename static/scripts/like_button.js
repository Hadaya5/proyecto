var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// import { publicacion } from "../components/publicacion";

var e = React.createElement;

var Publicacion = function (_React$Component) {
  _inherits(Publicacion, _React$Component);

  function Publicacion(props) {
    _classCallCheck(this, Publicacion);

    var _this = _possibleConstructorReturn(this, (Publicacion.__proto__ || Object.getPrototypeOf(Publicacion)).call(this, props));

    _this.state = { liked: false };

    _this.userDisplayName = 'hadaya hadaya';
    _this.userProfilePhoto = '/static/images/default/profile_icon.jpg';
    _this.media = '/static/images/david.jpg';
    _this.content = 'prueba de react';
    return _this;
  }

  _createClass(Publicacion, [{
    key: 'render',
    value: function render() {
      if (this.state.liked) {
        return 'You liked this.';
      }

      return e(React.createElement(
        IonCard,
        { id: 'publicacion' },
        React.createElement(
          'ion-card-header',
          null,
          React.createElement(
            'ion-item',
            { lines: 'none' },
            React.createElement(
              'ion-avatar',
              { slot: 'start' },
              React.createElement('img', { alt: 'Silhouette of a person\'s head', src: this.userProfilePhoto })
            ),
            React.createElement(
              'ion-card-title',
              null,
              this.userDisplayName
            ),
            React.createElement('h1', null)
          )
        ),
        React.createElement(
          'ion-card-content',
          null,
          React.createElement(
            'p',
            null,
            this.content
          ),
          this.media ? React.createElement('img', { 'class': 'media', alt: 'Silhouette of a person\'s head', src: this.media }) : ''
        )
      ));
    }
  }]);

  return Publicacion;
}(React.Component);

var LikeButton = function (_React$Component2) {
  _inherits(LikeButton, _React$Component2);

  function LikeButton(props) {
    _classCallCheck(this, LikeButton);

    var _this2 = _possibleConstructorReturn(this, (LikeButton.__proto__ || Object.getPrototypeOf(LikeButton)).call(this, props));

    _this2.state = { liked: false };
    return _this2;
  }

  _createClass(LikeButton, [{
    key: 'render',
    value: function render() {
      var _this3 = this;

      if (this.state.liked) {
        return 'You liked this.';
      }

      return e('button', { onClick: function onClick() {
          return _this3.setState({ liked: true });
        } }, 'Like');
    }
  }]);

  return LikeButton;
}(React.Component);

var domContainer = document.querySelector('#like_button_container');
console.log(domContainer);
var root = ReactDOM.createRoot(domContainer);
root.render(React.createElement(
  React.Fragment,
  null,
  React.createElement(
    'h1',
    null,
    'Prueba'
  ),
  React.createElement(Publicacion, null)
));