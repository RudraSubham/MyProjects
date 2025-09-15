import React from "react";
import styled from "styled-components";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Box } from "@mui/material";

const Card = styled.div`
  flex: 1;
  min-width: 280px;
  padding: 24px;
  border: 1px solid ${({ theme }) => theme.text_primary + "20"};
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
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

const COLORS = ["#1976d2"];

const WeeklyStatCard = ({ data }) => {
  if (!data?.totalWeeksCaloriesBurnt) return null;

  const chartData = data.totalWeeksCaloriesBurnt.weeks.map((week, index) => ({
    name: week,
    value: data.totalWeeksCaloriesBurnt.caloriesBurned[index] || 0,
  }));

  return (
    <Card>
      <Title>Weekly Calories Burned</Title>
      <Box sx={{ width: "100%", height: 300 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill={COLORS[0]} />
          </BarChart>
        </ResponsiveContainer>
      </Box>
    </Card>
  );
};

export default WeeklyStatCard;
