package com.example.mdp.map;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;

import androidx.annotation.Nullable;

import com.example.mdp.R;

import java.util.ArrayList;

public class Maze extends View {
    SharedPreferences sharedPreferences;
    private Paint black = new Paint();
    private Paint obstacleColor = new Paint();
    private Paint robotColor = new Paint();
    private Paint goalColor = new Paint();
    private Paint startPtColor = new Paint();
    private Paint wayptCoordColor = new Paint();
    private Paint unexploredCellColor = new Paint();
    private Paint exploredCellColor = new Paint();
    private Paint arrowColor = new Paint();
    private Paint fastestPathColor = new Paint();
    private boolean isDrawn = false;
    private static boolean canDrawRobot = false;


    private static String robotDirection = "None";
    private static int[] startCoord = new int[]{-1, -1};
    private static int[] curCoord = new int[]{-1, -1};
    private static int[] oldCoord = new int[]{-1, -1};
    private static int[] waypointCoord = new int[]{-1, -1};
    private static ArrayList<String[]> arrowCoord = new ArrayList<>();
    private static ArrayList<int[]> obstacleCoord = new ArrayList<>();
    private Bitmap arrowBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.ic_arrow_error);

    private static final int COL = 15;
    private static final int ROW = 20;
    private static float cellSize;
    private static Cell[][] cells;

    private boolean mapDrawn = false;
    public static String MDFExplorationString;
    public static String MDFObstacleString;

    public Maze(Context ctx){ //to initialise super class need ctx
        super(ctx);
    }


    public Maze(Context ctx, @Nullable AttributeSet att){
        super(ctx, att);
        black.setStyle(Paint.Style.FILL_AND_STROKE);
        obstacleColor.setColor(Color.BLACK);
        robotColor.setColor(Color.GREEN);
        goalColor.setColor(Color.RED);
        startPtColor.setColor(Color.CYAN);
        wayptCoordColor.setColor(Color.YELLOW);
        unexploredCellColor.setColor(Color.WHITE);
        arrowColor.setColor(Color.BLACK);
        fastestPathColor.setColor(Color.MAGENTA);
        sharedPreferences = getContext().getSharedPreferences("Shared Preferences", Context.MODE_PRIVATE);
    }

    private void initMap() {
        setWillNotDraw(false);
    }


    @Override
    protected void onDraw(Canvas canvas){
        super.onDraw(canvas);
        if(!isDrawn){
            String[] dummyArrowCoord = new String[3];
            dummyArrowCoord[0] = "1";
            dummyArrowCoord[1] = "1";
            dummyArrowCoord[2] = "dummy";
            arrowCoord.add(dummyArrowCoord);
            this.createCell();
            this.setEndCoordinate(14, 19);
            isDrawn = true;
        }

        drawCell(canvas);
        drawHorizontalLines(canvas);
        drawVerticalLines(canvas);
        drawGridNumber(canvas);
    }

    private class Cell {
        float startX, startY, endX, endY;
        Paint paint;
        String type;
        int id = -1;

        private Cell(float startX, float startY, float endX, float endY, Paint paint, String type) {
            this.startX = startX;
            this.startY = startY;
            this.endX = endX;
            this.endY = endY;
            this.paint = paint;
            this.type = type;
        }

        public void setType(String type) {
            this.type = type;
            switch (type) {
                case "obstacle":
                    this.paint = obstacleColor;
                    break;
                case "robot":
                    this.paint = robotColor;
                    break;
                case "end":
                    this.paint = goalColor;
                    break;
                case "start":
                    this.paint = startPtColor;
                    break;
                case "waypoint":
                    this.paint = wayptCoordColor;
                    break;
                case "unexplored":
                    this.paint = unexploredCellColor;
                    break;
                case "explored":
                    this.paint = exploredCellColor;
                    break;
                case "arrow":
                    this.paint = arrowColor;
                    break;
                case "fastestPath":
                    this.paint = fastestPathColor;
                    break;
                case "image":
                    this.paint = obstacleColor;
                default:
                    break;
            }
        }

        public void setId(int id) {
            this.id = id;
        }

        public int getId() {
            return this.id;
        }
    }

    private void createCell() {//creates
        cells = new Cell[COL + 1][ROW + 1]; //15 + 1 and 20 + 1, this creates 0 to 15 and 0 to 20, one extra cell for the grid numbers
        this.calculateDimension();
        cellSize = this.getCellSize();

        for (int x = 0; x <= COL; x++)
            for (int y = 0; y <= ROW; y++)
                cells[x][y] = new Cell(x * cellSize + (cellSize / 50), y * cellSize + (cellSize / 50), (x + 1) * cellSize, (y + 1) * cellSize, unexploredCellColor, "unexplored");
    }

    public void setEndCoordinate(int col, int row) { //sets the top right corner of the endGoal cells
        row = this.convertRow(row); //returns 20-19 = 1
        for (int x = col - 1; x <= col + 1; x++) //14 - 1 = 13 to 15
            for (int y = row - 1; y <= row + 1; y++) //0 to 2
                cells[x][y].setType("end");
    }


    private void drawCell(Canvas canvas) {
        for (int x = 1; x <= COL; x++)
            for (int y = 0; y < ROW; y++)
                for (int i = 0; i < this.getArrowCoord().size(); i++)
                    if (!cells[x][y].type.equals("image") && cells[x][y].getId() == -1) {
                        canvas.drawRect(cells[x][y].startX, cells[x][y].startY, cells[x][y].endX, cells[x][y].endY, cells[x][y].paint);
                    } else {
//                        Paint textPaint = new Paint();
//                        textPaint.setTextSize(20);
//                        textPaint.setColor(Color.WHITE);
//                        textPaint.setTextAlign(Paint.Align.CENTER);
//                        canvas.drawRect(cells[x][y].startX, cells[x][y].startY, cells[x][y].endX, cells[x][y].endY, cells[x][y].paint);
//                        canvas.drawText(String.valueOf(cells[x][y].getId()),(cells[x][y].startX+cells[x][y].endX)/2, cells[x][y].endY + (cells[x][y].startY-cells[x][y].endY)/4, textPaint);
                    }

    }

    private void drawHorizontalLines(Canvas canvas) {
        for (int y = 0; y <= ROW; y++)
            canvas.drawLine(cells[1][y].startX, cells[1][y].startY - (cellSize / 30), cells[15][y].endX, cells[15][y].startY - (cellSize / 30), black);
    }

    private void drawVerticalLines(Canvas canvas) {
        for (int x = 0; x <= COL; x++)
            canvas.drawLine(cells[x][0].startX - (cellSize / 30) + cellSize, cells[x][0].startY - (cellSize / 30), cells[x][0].startX - (cellSize / 30) + cellSize, cells[x][19].endY + (cellSize / 30), black);
    }

    private void drawGridNumber(Canvas canvas) {
        for (int x = 1; x <= COL; x++) {
            if (x > 9)
                canvas.drawText(Integer.toString(x-1), cells[x][20].startX + (cellSize / 5), cells[x][20].startY + (cellSize / 3), black);
            else
                canvas.drawText(Integer.toString(x-1), cells[x][20].startX + (cellSize / 3), cells[x][20].startY + (cellSize / 3), black);
        }
        for (int y = 0; y < ROW; y++) {
            if ((20 - y) > 9)
                canvas.drawText(Integer.toString(19 - y), cells[0][y].startX + (cellSize / 2), cells[0][y].startY + (cellSize / 1.5f), black);
            else
                canvas.drawText(Integer.toString(19 - y), cells[0][y].startX + (cellSize / 1.5f), cells[0][y].startY + (cellSize / 1.5f), black);
        }
    }

    private void calculateDimension() {
        this.setCellSize(getWidth()/(COL+1));
    }

    private void setCellSize(float cellSize) {
        Maze.cellSize = cellSize;
    }

    private float getCellSize() {
        return cellSize;
    }

    private ArrayList<String[]> getArrowCoord() {
        return arrowCoord;
    }

    private int convertRow(int row) {
        return (20 - row);
    }






    public boolean getCanDrawRobot() {
        return canDrawRobot;
    }

}
