import React, { useEffect, useState } from 'react';

interface SensorData {
  sensor_id: string;
  value: number;
  unit: string;
  status: string;
  timestamp: string;
}

export default function App() {
  const [readings, setReadings] = useState<SensorData[]>([]);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [mode, setMode] = useState<'websocket' | 'polling'>('websocket');

  // OPCIÓN A: Consulta REST tradicional mediante setInterval (cada 5 segundos)
  useEffect(() => {
    if (mode !== 'polling') return;

    const fetchRestData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/readings/');
        if (!response.ok) throw new Error('Error en la respuesta de la API');
        const data = await response.json();
        setReadings(data);
        setIsConnected(true); // Hay conexión con el backend
      } catch (error) {
        console.error("Error al consultar la API REST:", error);
        setIsConnected(false); // Sin comunicación
      }
    };

    fetchRestData();
    const interval = setInterval(fetchRestData, 5000);
    return () => clearInterval(interval);
  }, [mode]);

  // OPCIÓN B: Conexión en tiempo real mediante WebSockets (Django Channels)
  useEffect(() => {
    if (mode !== 'websocket') return;

    const ws = new WebSocket('ws://127.0.0.1:8000/ws/scada/');

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const newReading: SensorData = JSON.parse(event.data);
      setReadings((prev) => [newReading, ...prev.slice(0, 19)]); // Mantiene las últimas 20 lecturas
    };

    ws.onerror = (error) => {
      console.error("Error en WebSocket:", error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false); // Dispara la alerta visual de desconexión
    };

    return () => {
      ws.close();
    };
  }, [mode]);

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial, sans-serif', background: '#f4f6f8', minHeight: '100vh' }}>
      <h1>Panel SCADA Industrial - Tiempo Real</h1>

      {/* Alerta Visual Clara de Desconexión */}
      {!isConnected && (
        <div style={{ background: '#ff4d4f', color: 'white', padding: '15px', borderRadius: '5px', marginBottom: '20px', fontWeight: 'bold' }}>
          ⚠️ Sin comunicación con el SCADA / Servidor o WebSocket desconectado. Intentando reconectar...
        </div>
      )}

      {/* Selector de modo para pruebas */}
      <div style={{ marginBottom: '20px', background: 'white', padding: '15px', borderRadius: '8px', display: 'inline-block' }}>
        <label style={{ marginRight: '10px', fontWeight: 'bold' }}>Modo de comunicación: </label>
        <button 
          onClick={() => setMode('websocket')} 
          style={{ background: mode === 'websocket' ? '#1890ff' : '#ccc', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '4px', marginRight: '10px', cursor: 'pointer' }}>
          Tiempo Real (WebSockets)
        </button>
        <button 
          onClick={() => setMode('polling')} 
          style={{ background: mode === 'polling' ? '#1890ff' : '#ccc', color: 'white', border: 'none', padding: '8px 12px', borderRadius: '4px', cursor: 'pointer' }}>
          API REST Tradicional (setInterval)
        </button>
      </div>

      {/* Tarjetas de Sensores */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
        {readings.map((item, index) => (
          <div key={index} style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>{item.sensor_id}</h3>
            <p style={{ fontSize: '28px', fontWeight: 'bold', margin: '10px 0', color: '#111' }}>
              {item.value} <span style={{ fontSize: '16px', color: '#666' }}>{item.unit}</span>
            </p>
            <p style={{ margin: '5px 0' }}>
              Estado: <span style={{ color: item.status === 'OK' ? '#52c41a' : '#ff4d4f', fontWeight: 'bold' }}>{item.status}</span>
            </p>
            <small style={{ color: '#999' }}>{new Date(item.timestamp).toLocaleTimeString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
}