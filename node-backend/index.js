const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
app.use(cors());            // permite llamadas desde el navegador
app.use(express.json());    // parsea JSON del body

// ⚠️ Credenciales: deben coincidir con tu docker-compose (user/pass/db)
const pool = new Pool({
  user: 'shadow',
  host: 'localhost',   // estamos fuera de Docker, usamos el puerto publicado
  database: 'clips',
  password: 'shadow',
  port: 5432
});

// Ruta para insertar un link
app.post('/links', async (req, res) => {
  try {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'url requerida' });

    const result = await pool.query(
      'INSERT INTO links (url) VALUES ($1) RETURNING *',
      [url]
    );
    res.json(result.rows[0]);
  } catch (err) {
	    console.error(err);
    res.status(500).json({ error: 'error insertando link' });
  }
});

// Ruta para obtener todos los links
app.get('/links', async (_req, res) => {
  try {
    const result = await pool.query('SELECT * FROM links ORDER BY id DESC');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'error listando links' });
  }
});

// Salud
app.get('/', (_req, res) => {
  res.json({ ok: true, service: 'shadowclip-node' });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
