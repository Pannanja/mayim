import './App.css';
import ChatBox from './components/ChatBox';
import BibleBrowser from './components/BibleBrowser';
import ReferenceList from './components/ReferenceList';
import { CurrentChapterProvider } from './context/CurrentChapterContext';
import { ReferenceProvider } from './context/ReferenceContext';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ReferenceProvider>
          <CurrentChapterProvider>
            <ChatBox />
            <ReferenceList />
            <BibleBrowser />
          </CurrentChapterProvider>
        </ReferenceProvider>
      </header>
    </div>
  );
}

export default App;