// server.js
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;
const TRACKINGMORE_API_KEY = 'your-trackingmore-api-key';

app.use(express.json());

app.post('/trackCargo', async (req, res) => {
    const { waybillNumber } = req.body;
    try {
        const response = await axios.get(`https://api.trackingmore.com/v2/trackings/realtime?numbers=${waybillNumber}`, {
            headers: {
                'Content-Type': 'application/json',
                'Trackingmore-Api-Key': TRACKINGMORE_API_KEY
            }
        });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
