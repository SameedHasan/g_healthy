import React, { useEffect, useState } from "react";
import { useFrappeAuth } from "frappe-react-sdk";
import { Button, Input, Form, Alert, Card, Checkbox } from "antd";
// import { useLocation, useNavigate } from "react-router-dom";
import { LogoIcon } from "../../utils/icons";

const LoginForm = () => {
  const { login, isLoading, error, currentUser } = useFrappeAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  // const navigate = useNavigate()
  // const location = useLocation()
  // const from = location.state?.from?.pathname || "/dashboard";
  const handleLogin = () => {
    login({ username, password });
  };
  useEffect(() => {
    if (currentUser) {
      window.location.replace("/dashboard");
    }
  }, [currentUser])

  return (
    <div style={{ maxWidth: 560, margin: "auto", display: "flex", flexDirection: "column", justifyContent: "center", height: "100vh" }}>
      <Card className="login-card" style={{ borderRadius: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.04)", padding: 0 }}>
        <div className="login-icon">
          {/* <LogoIcon style={{ marginBottom: 8 }} /> */}
          {/* <img src={loginImage} alt="logo" style={{ width: "auto", height: "50px" }} /> */}
        </div>
        <div className="login-card-header" >
          <h2 className="login-card-title">Login</h2>
          <p className="login-card-subtitle">Welcome back! Please enter your details.</p>
        </div>
        <Form onFinish={handleLogin} layout="vertical" style={{ marginBottom: 0 }}>
          <Form.Item label={<span>Email</span>} style={{ marginBottom: 20 }}>
            <Input
              placeholder="Enter email address"
              value={username}
              onChange={e => setUsername(e.target.value)}
              type="text"
              autoComplete="username"
            />
          </Form.Item>
          <Form.Item label={<span> Password</span>} style={{ marginBottom: 56 }}>
            <Input.Password
              placeholder="Enter password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0 }}>
            <Button type="primary" htmlType="submit" loading={isLoading} block className="atn-btn btn-lg" disabled={!username || !password}>
              Login
            </Button>
          </Form.Item>
          {error && <Alert message={error.message} type="error" style={{ marginTop: 12 }} />}
        </Form>

      </Card>
    </div>
  );
};

export default LoginForm;
