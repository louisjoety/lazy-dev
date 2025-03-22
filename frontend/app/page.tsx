import { Main } from 'next/document';
import LoginForm from './components/pages/LoginForm';
import MainPage from './components/pages/DragAndDrop';
import Chatbot from './components/pages/Chatbot';
import DragAndDrop from './components/pages/DragAndDrop';
import Dashboard from './components/pages/Dashboard';

export default function Page() {
  return (
    <div>
      {/*<LoginForm />*/}
      {/*<MainPage />*/}
      {/*<Chatbot />*/}
      {/* <DragAndDrop /> */}
      <Dashboard files={[]} /> 
    </div>
  );
}
