import React, { useState } from "react";
import axios from "axios";

const ProxyList = () => {
    const [proxies, setProxies] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchProxies = (update = false) => {
        setLoading(true);
        const url = update
            ? "http://127.0.0.1:5000/update-proxies" // مسیر به‌روزرسانی
            : "http://127.0.0.1:5000/proxies"; // مسیر دریافت لیست

        const method = update ? "POST" : "GET"; // متد درخواست

        axios({
            method: method,
            url: url,
        })
            .then((response) => setProxies(Object.values(response.data)))
            .catch((error) => console.error("Error fetching proxies:", error))
            .finally(() => setLoading(false));
    };

    return (
        <div className="container">
            <h1>لیست پراکسی‌ها</h1>
            <div className="buttons">
                <button onClick={() => fetchProxies(false)}>دریافت لیست</button>
                <button onClick={() => fetchProxies(true)}>به‌روزرسانی لیست</button>
            </div>
            {loading ? (
                <p>در حال بارگذاری...</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Link</th>
                            <th>IP</th>
                            <th>Port</th>
                        </tr>
                    </thead>
                    <tbody>
                        {proxies.map((proxy, index) => (
                            <tr key={index}>
                                <td>{proxy.link}</td>
                                <td>{proxy.IP}</td>
                                <td>{proxy.Port}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default ProxyList;
