import './App.css';
import ChatBox from './components/ChatBox/ChatBox';
import BibleBrowser from './components/BibleBrowser/BibleBrowser';
import ReferenceList from './components/ReferenceList/ReferenceList';
import { CurrentChapterProvider } from './context/CurrentChapterContext';
import { ReferenceProvider } from './context/ReferenceContext';
import Wonderings from './components/Wonderings/Wonderings';

function App() {
  const handleAddToChat = (question) => {
    // Implement the logic to add the question to the chat box input
    // This could involve using a state management solution like Redux or Context API
  };

  return (
    <div className="App">
      <header className="App-header">
        <ReferenceProvider>
          <CurrentChapterProvider>
            <div className="Stars">
              <div className="Wonderings-left">
                <Wonderings onAddToChat={handleAddToChat} />
              </div>
              <ChatBox />
              <div className="Wonderings-right">
                <Wonderings onAddToChat={handleAddToChat} />
              </div>
            </div>
            <div className="Clouds">
              <ReferenceList />
            </div>
            <div className="Stones">
              <BibleBrowser />
            </div>
          </CurrentChapterProvider>
        </ReferenceProvider>
      </header>
    </div>
  );
}

export default App;