import React, { useState } from "react";
import {
  Row,
  Col,
  Card,
  Statistic,
  Table,
  Progress,
  Typography,
  Button,
  DatePicker,
} from "antd";
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  ReloadOutlined,
  CalendarOutlined,
} from "@ant-design/icons";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import "./index.css";
import {
  CheckIcon,
  DownArrowCircleIcon,
  NoteIcon,
  UpArrowCircleIcon,
  UsersIcon,
} from "../../utils/icons";

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;

// Mock data for the dashboard
const mockData = {
  totalUsers: 1250,
  totalUsersChange: 12,
  goalsCompletionRate: 76,
  goalsCompletionChange: -12,
  totalLessonsView: 680,
  totalLessonsViewChange: 12,

  weightLoggingData: [
    { month: "Jan", value: 160 },
    { month: "Feb", value: 200 },
    { month: "Mar", value: 220 },
    { month: "Apr", value: 180 },
    { month: "May", value: 240 },
    { month: "Jun", value: 250 },
  ],

  topGoalsCompleted: [
    { name: "Meal Planning & Preparation", percentage: 85 },
    { name: "Caloric Awareness", percentage: 82 },
    { name: "Resistance Training", percentage: 78 },
    { name: "Flexibility & Mobility Work", percentage: 74 },
  ],

  usersByCity: [
    { name: "Baton Rouge", percentage: 33 },
    { name: "New Orleans", percentage: 19 },
    { name: "Lafayette", percentage: 15 },
    { name: "Others", percentage: 33 },
  ],

  topLessonsViewed: [
    { name: "Meal Planning & Preparation", users: 3200, completionRate: 92 },
    { name: "Caloric Awareness", users: 2900, completionRate: 87 },
    { name: "Resistance Training", users: 2700, completionRate: 78 },
    { name: "Flexibility & Mobility Work", users: 2650, completionRate: 70 },
    { name: "Sleep Optimization", users: 2400, completionRate: 68 },
  ],
};

const Dashboard = () => {
  const [loading, setLoading] = useState(false);

  // Function to refresh data
  const refreshData = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  // Weight logging chart options
  const weightChartOptions = {
    chart: {
      type: "area",
      height: 315,
      backgroundColor: "transparent",
    },
    title: {
      text: null,
    },
    xAxis: {
      categories: mockData.weightLoggingData.map((item) => item.month),
    },
    yAxis: {
      title: {
        text: null,
      },
      tickInterval: 50,
      max: 250,
      min: 0,
    },
    tooltip: {
      crosshairs: true,
      shared: true,
    },
    plotOptions: {
      area: {
        fillColor: {
          linearGradient: [0, 0, 0, 130],
          stops: [
            [0, "rgba(128,99,255,0.4)"],
            [1, "rgba(128,99,255,0)"],
          ],
        },
        showInLegend: false,
        marker: {
          enabled: false,
        },
      },
    },
    series: [
      {
        name: "Weight Logs",
        color: "#8676FF",
        data: mockData.weightLoggingData.map((item) => item.value),
      },
    ],
    credits: {
      enabled: false,
    },
  };

  // Users by city pie chart options
  const cityChartOptions = {
    chart: {
      type: "pie",
      height: 250,
    },
    title: {
      text: null,
    },
    tooltip: {
      pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: "pointer",
        dataLabels: {
          enabled: false,
        },
        showInLegend: true,
      },
    },
    series: [
      {
        name: "Users",
        colorByPoint: true,
        data: mockData.usersByCity.map((city) => ({
          name: city.name,
          y: city.percentage,
        })),
      },
    ],
    colors: ["#00C49F", "#8676FF", "#00A3FF", "#FF6B6B"],
    credits: {
      enabled: false,
    },
  };

  // Table columns for top lessons
  const columns = [
    {
      title: "Lesson Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Users",
      dataIndex: "users",
      key: "users",
      sorter: (a, b) => a.users - b.users,
    },
    {
      title: "Completion Rate",
      dataIndex: "completionRate",
      key: "completionRate",
      sorter: (a, b) => a.completionRate - b.completionRate,
      render: (rate) => `${rate}%`,
    },
  ];

  return (
    <div className="dashboard-container">
      {/* Stats cards */}
      <Row gutter={[30, 30]} className="stats-row" align="stretch">
        <Col xs={24} sm={8} style={{ display: "flex" }}>
          <Card loading={loading} className="stat-card">
            <div className="stat-card-content">
              <div className="stat-card-content-left">
                <div className="stat-card-content-left-item">
                  <span className="stat-title">Total Users</span>
                  <div className="stat-value">1,250</div>
                </div>
                <div className="stat-change positive">
                  <UpArrowCircleIcon />
                  <span className="stat-change-value">12%</span>
                  <span className="stat-change-desc">(42 users)</span>
                </div>
              </div>
              <div>
                <span className="stat-icon">
                  <UsersIcon bg />
                </span>
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={8} style={{ display: "flex" }}>
          <Card loading={loading} className="stat-card">
            <div className="stat-card-content">
              <div className="stat-card-content-left">
                <div className="stat-card-content-left-item">
                  <span className="stat-title">Goals Completion Rate</span>
                  <div className="stat-value">76%</div>
                </div>
                <div className="stat-change negative">
                  <DownArrowCircleIcon />
                  <span className="stat-change-value">1.2%</span>
                  <span className="stat-change-desc">(12 lessons)</span>
                </div>
              </div>
              <div>
                <span className="stat-icon">
                  <CheckIcon bg />
                </span>
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={8} style={{ display: "flex" }}>
          <Card loading={loading} className="stat-card">
            <div className="stat-card-content">
              <div className="stat-card-content-left">
                <div className="stat-card-content-left-item">
                  <span className="stat-title">Total Lessons view</span>
                  <div className="stat-value">680</div>
                </div>
                <div className="stat-change positive">
                  <UpArrowCircleIcon />
                  <span className="stat-change-value">1.2%</span>
                  <span className="stat-change-desc">(24 responses)</span>
                </div>
              </div>
              <div>
                <span className="stat-icon">
                  <NoteIcon bg />
                </span>
              </div>
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={14} style={{ display: "flex" }}>
          <Card
            title="Users Logging Weight"
            bordered={false}
            loading={loading}
            style={{ flex: 1 }}
          >
            <HighchartsReact
              highcharts={Highcharts}
              options={weightChartOptions}
            />
          </Card>
        </Col>
        <Col xs={24} lg={10} style={{ display: "flex" }}>
          <Card
            title="Top Goals Completed"
            bordered={false}
            loading={loading}
            style={{ flex: 1 }}
          >
            {mockData.topGoalsCompleted.map((goal, index) => (
              <div key={index} className="goal-progress-item">
                <div className="goal-info">
                  <Text>{goal.name}</Text>
                  <Text strong>{`${goal.percentage}%`}</Text>
                </div>
                <Progress
                  percent={goal.percentage}
                  showInfo={false}
                  strokeColor="#8676FF"
                  trailColor="#F0F0F0"
                />
              </div>
            ))}
          </Card>
        </Col>
        <Col xs={24} lg={8} style={{ display: "flex" }}>
          <Card
            title="Users by City"
            bordered={false}
            loading={loading}
            style={{ flex: 1 }}
          >
            <HighchartsReact
              highcharts={Highcharts}
              options={cityChartOptions}
            />
            <div className="chart-legend">
              {mockData.usersByCity.map((city, index) => (
                <div key={index} className="legend-item">
                  <span className={`legend-color color-${index}`}></span>
                  <Text>{city.name}</Text>
                  <Text strong>{`${city.percentage}%`}</Text>
                </div>
              ))}
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={16} style={{ display: "flex" }}>
          <Card
            title="Top Lessons Viewed"
            bordered={false}
            loading={loading}
            extra={
              <Button type="link" size="small">
                View all
              </Button>
            }
            style={{ flex: 1 }}
          >
            <Table
              dataSource={mockData.topLessonsViewed}
              columns={columns}
              pagination={false}
              rowKey="name"
              loading={loading}
              size="middle"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
