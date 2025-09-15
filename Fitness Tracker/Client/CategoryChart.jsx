import React from "react";
import styled from "styled-components";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Box } from "@mui/material";

const Card = styled.div`
  flex: 1;
  min-width: 280px;
  padding: 24px;
  border: 1px solid ${({ theme }) => theme.text_primary + "20"};
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 1px 6px 20px 0px ${({ theme }) => theme.primary + "15"};
  @media (max-width: 600px) {
    padding: 16px;
  }
`;

const Title = styled.div`
  font-weight: 600;
  font-size: 16px;
  color: ${({ theme }) => theme.primary};
`;

const COLORS = ["#1976d2", "#dc004e", "#ff9800", "#4caf50", "#9c27b0"];

const CategoryChart = ({ data }) => {
  if (!data?.pieChartData || data.pieChartData.length === 0) return null;

  return (
    <Card>
      <Title>Weekly Calories Burned</Title>
      <Box sx={{ width: "100%", height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data.pieChartData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={100}
              paddingAngle={5}
              cornerRadius={5}
            >
              {data.pieChartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </Box>
    </Card>
  );
};

export default CategoryChart;
