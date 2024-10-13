import logo from './logo.svg';
import './App.css';
import AppLayout from './components/AppLayout';
import ChatBox from './components/ChatBox';
import BookList from './components/BookList';
import TranslationList from './components/TranslationList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ChatBox></ChatBox>
        <TranslationList></TranslationList>
      </header>
    </div>
  );
}

export default App;
