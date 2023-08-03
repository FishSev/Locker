import React, { useEffect, useState } from 'react';

import axios from 'axios';
import './App.css';

const LockerComponent = () => {
  const [doorState, setDoorState] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleUnlock = async () => {
    try {
      const response = await axios.post('https://madenews.me:5000/unlock', { password: { password } });
      setDoorState(response.data.state);
      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
    }
  };

  const handleLock = async () => {
    try {
      const response = await axios.post('https://madenews.me:5000/lock');

      setPassword('')
      setDoorState(response.data.state);
      setMessage(response.data.message);
    } catch (error) {
      console.error(error);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleUnlock();
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('https://madenews.me:5000/');
        setDoorState(response.data.state);
        setMessage(response.data.message);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, []);

  const reloadInterval = 60 * 1000;

  useEffect(() => {
    const reloadPage = () => {
      window.location.reload();
    };

    const reloadTimer = setInterval(reloadPage, reloadInterval);

    return () => clearInterval(reloadTimer);
  }, [reloadInterval]);

  return (
    <div className="App">
      <h1>Камера хранения</h1>
      <p>{message}</p>
      {doorState === 'locked' && <button onClick={handleUnlock}>Открыть замок</button>}

      {doorState === 'unlocked' && <button onClick={handleLock}>Закрыть замок</button>}

      {doorState === 'locked' && <input type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        onKeyDown={handleKeyPress}
      />}


    </div>


  );
};


export default LockerComponent;
