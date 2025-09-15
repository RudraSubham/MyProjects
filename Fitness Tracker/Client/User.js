import express from "express";
import {
  UserRegister,
  UserLogin,
  getUserDashboard,
  getWorkoutsByDate,
  addWorkout,
} from "../controllers/User.js";
import { verifyToken } from "../middleware/verifyToken.js";

const router = express.Router();

// Register
router.post("/signup", UserRegister);

// Login
router.post("/signin", UserLogin);

// Dashboard (protected)
router.get("/dashboard", verifyToken, getUserDashboard);

// Get workouts by date (protected)
router.get("/workouts", verifyToken, getWorkoutsByDate);

// Add workout (protected)
router.post("/workouts", verifyToken, addWorkout);

export default router;
