import './App.css';
import ChatBox from './components/ChatBox';
import BibleBrowser from './components/BibleBrowser';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ChatBox></ChatBox>
        <BibleBrowser></BibleBrowser>
      </header>
    </div>
  );
}

export default App;
