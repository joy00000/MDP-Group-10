package com.example.mdp.map;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Rect;
import android.graphics.Typeface;
import android.util.AttributeSet;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.core.view.GestureDetectorCompat;

import com.example.mdp.MainActivity;
import com.example.mdp.R;

import java.io.Serializable;
import java.util.ArrayList;


public class Maze extends View implements Serializable {

    private static final String TAG = "Arena Map";

    private static Cell[][] cells;
    private static final int COLS = 20, ROWS = 20;
    private static float cellSize, hMargin, vMargin;
    private static String robotDirection = "north";
    private static int[] obsCoord = new int[]{-1, -1};
    private static int[] curCoord = new int[]{-1, -1};
    private static int[] oldCoord = new int[]{-1, -1};
    private static ArrayList<int[]> obstacleCoord = new ArrayList<>();

    private static Obstacle [] obstacleList = new Obstacle[8];

    private static Paint wallPaint = new Paint();
    private static Paint robotPaint = new Paint();
    private static Paint directionPaint = new Paint();
    private static Paint obstaclePaint = new Paint();
    private static Paint unexploredPaint = new Paint();
    private static Paint exploredPaint = new Paint();
    private static Paint gridNumberPaint = new Paint();
    private static Paint obstacleNumberPaint = new Paint();
    private static Paint emptyPaint = new Paint();
    private static Paint virtualWallPaint = new Paint();

    private static Paint westPaint = new Paint();
    private static Paint eastPaint = new Paint();
    private static Paint southPaint = new Paint();
    private static Paint northPaint = new Paint();
    private static Paint linePaint = new Paint();

    //Create only avail when state is true
    private static boolean createCellStatus = false;
    private static boolean setRobotPostition = false;
    private static boolean changedFaceAnnotation = false;
    private static boolean validPosition = false;
    private static boolean canDrawRobot = false;
//    private static boolean canDrawObstacle = false;
//    private static boolean canUpdateObsFace = false;
//    private static boolean canDrag = false;
//    private static boolean isOnClick = false;

    private View mapView;
    private Rect r;

//    private static final int MAX_CLICK_DURATION = 200;
//    private long mStartClickTime;

    private GestureDetectorCompat mGestureDetector;
    private LongPressGestureListener longPressGestureListener;


    public Maze(Context context) {
        super(context);
        init(null);
    }

    public Maze(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init(attrs);

        wallPaint.setColor(Color.WHITE);
        robotPaint.setColor(Color.parseColor("#bada55"));
        directionPaint.setColor(Color.BLACK);
        unexploredPaint.setColor(Color.parseColor("#ccd8d7"));
        exploredPaint.setColor(Color.GRAY);
        emptyPaint.setColor(Color.WHITE);
        virtualWallPaint.setColor(Color.parseColor("#FFA500"));

        obstaclePaint.setColor(Color.BLACK);
        obstaclePaint.setStyle(Paint.Style.FILL);
        obstaclePaint.setStrokeWidth(3f);

        obstacleNumberPaint.setColor(Color.WHITE);
        obstacleNumberPaint.setTextSize(20);
        obstacleNumberPaint.setTypeface(Typeface.DEFAULT_BOLD);
        obstacleNumberPaint.setAntiAlias(true);
        obstacleNumberPaint.setStyle(Paint.Style.FILL);
        obstacleNumberPaint.setTextAlign(Paint.Align.LEFT);

        gridNumberPaint.setColor(Color.BLACK);
        gridNumberPaint.setTextSize(15);
        gridNumberPaint.setStyle(Paint.Style.FILL_AND_STROKE);

        westPaint.setColor(Color.GREEN);
        westPaint.setStyle(Paint.Style.FILL);

        eastPaint.setColor(Color.RED);
        eastPaint.setStyle(Paint.Style.FILL);

        northPaint.setColor(Color.YELLOW);
        northPaint.setStyle(Paint.Style.FILL);

        southPaint.setColor(Color.BLUE);
        southPaint.setStyle(Paint.Style.FILL);

        linePaint.setStyle(Paint.Style.STROKE);
        linePaint.setColor(Color.YELLOW);
        linePaint.setStrokeWidth(3f);

        longPressGestureListener = new LongPressGestureListener(this.mapView);
        mGestureDetector = new GestureDetectorCompat(context, longPressGestureListener);

        obstacleList [0] = new Obstacle (670, 40, 670, 40,"1", 0, "None","1");
        obstacleList [1] = new Obstacle(670, 115, 670, 115,"2", 0, "None", "2");
        obstacleList [2] = new Obstacle(670, 190, 670, 190,"3", 0, "None", "3");
        obstacleList [3] = new Obstacle(670, 265, 670, 265,"4", 0, "None", "4");
        obstacleList [4] = new Obstacle(670, 340, 670, 340,"5", 0, "None", "5");
        obstacleList [5] = new Obstacle(670, 410, 670, 410,"6", 0, "None", "6");
        obstacleList [6] = new Obstacle(670, 485, 670, 485,"7", 0, "None", "7");
        obstacleList [7] = new Obstacle(670, 565, 670, 565,"8", 0, "None", "8");

    }

    private void init(@Nullable AttributeSet set){
    }

    //Create Cell method
    private void createCells(){
        cells = new Cell[COLS][ROWS];
        for (int x = 0; x < COLS; x++) {
            for (int y = 0; y < ROWS; y++) {

                cells[x][y] = new Cell(x * cellSize + (cellSize / 30),
                        y * cellSize + (cellSize / 30),
                        (x + 1) * cellSize - (cellSize / 40),
                        (y + 1) * cellSize - (cellSize / 60), unexploredPaint);

                float xMiddle = ((((x + 1) * cellSize - (cellSize / 40))-(x * cellSize + (cellSize / 30)))/2);
                float yMiddle =  ((((y + 1) * cellSize - (cellSize / 60))-(y * cellSize + (cellSize / 30)))/2);
                Log.d(TAG, "CreateCell XMid" + xMiddle);
                Log.d(TAG, "CreateCell YMid" + yMiddle);

            }
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        super.onTouchEvent(event);
        int coordinates[];
        int x = (int) event.getX();
        int y = (int) event.getY();

        mGestureDetector.onTouchEvent(event);

        //Get touched coordinate
        coordinates = findGridOnTouch(x, y);

        Log.d(TAG, "onTouchEvent: Touched coordinates are " +
                coordinates[0] + " " + coordinates[1]);

        Log.d(TAG, "onTouchEvent: Touched coordinates are " +
                x + " " + y);

        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                //Touch down code
                Log.d(TAG, "onTouchEvent: ACTION_DOWN");
                for (int i = 0; i < obstacleList.length; i++) {
                    if (obstacleList[i].isTouched(x, y) && !obstacleList[i].getActionDown()) {
                        Log.d(TAG, "onTouchEvent: this is touched--->" + obstacleList[i].obsID);
                        Log.d(TAG, "onTouchEvent: Coordinates are " +
                                coordinates[0] + " " + coordinates[1]);

                        //Set new width and height (Resize the obstacle)
//                        obstacleList[i].setResizeUp(true);
                        obstacleList[i].setActionDown(true);
//                        if(!mGestureDetector.isLongpressEnabled()){
//                            obstacleList[i].setActionDown(true);
//                        } else {
//                            Log.d(TAG,"Enabled: " + mGestureDetector.isLongpressEnabled());
//                            obstacleList[i].setActionDown(false);
//                        }
                        //Add view to Main Activity to see where the obstacle's coordinates are at
                        invalidate();
                    }
                }
                break;
            case MotionEvent.ACTION_MOVE:
                Log.d(TAG, "onTouchEvent: ACTION_MOVE");

                MainActivity.setXCoord(coordinates[0]);


                if(coordinates[1] == 1){
                    MainActivity.setyCoord(19);
                }
                if(coordinates[1] == 2){
                    MainActivity.setyCoord(18);
                }
                if(coordinates[1] == 3){
                    MainActivity.setyCoord(17);
                }
                if(coordinates[1] == 4){
                    MainActivity.setyCoord(16);
                }
                if(coordinates[1] == 5){
                    MainActivity.setyCoord(15);
                }
                if(coordinates[1] == 6){
                    MainActivity.setyCoord(14);
                }
                if(coordinates[1] == 7){
                    MainActivity.setyCoord(13);
                }
                if(coordinates[1] == 8){
                    MainActivity.setyCoord(12);
                }
                if(coordinates[1] == 9){
                    MainActivity.setyCoord(11);
                }
                if(coordinates[1] == 10){
                    MainActivity.setyCoord(10);
                }
                if(coordinates[1] == 11){
                    MainActivity.setyCoord(9);
                }
                if(coordinates[1] == 12){
                    MainActivity.setyCoord(8);
                }
                if(coordinates[1] == 13){
                    MainActivity.setyCoord(7);
                }
                if(coordinates[1] == 14){
                    MainActivity.setyCoord(6);
                }
                if(coordinates[1] == 15){
                    MainActivity.setyCoord(5);
                }
                if(coordinates[1] == 16){
                    MainActivity.setyCoord(4);
                }
                if(coordinates[1] == 17){
                    MainActivity.setyCoord(3);
                }
                if(coordinates[1] == 18){
                    MainActivity.setyCoord(2);
                }
                if(coordinates[1] == 19){
                    MainActivity.setyCoord(1);
                }
                if(coordinates[1] == -1){
                    MainActivity.setyCoord(0);

                }
                if(coordinates[0]==-1){
                    MainActivity.setyCoord(-1);
                }

                //Movement of dragable obj
                for (Obstacle obstacles : obstacleList) {
                    if (obstacles.getActionDown()) {
                        Log.d(TAG, "C x: " + x);
                        Log.d(TAG, "C y: " + y);
                        Log.d(TAG, "C First (MOVE): " + coordinates[0]);
                        Log.d(TAG, "C Second (MOVE): " + coordinates[1]);
                        obstacles.setPosition(x, y);
                        invalidate();
                    }
                }
                break;
            case MotionEvent.ACTION_UP:
                Log.d(TAG, "onTouchEvent: ACTION_UP");
                //Code for releasing finger
                for (Obstacle obstacles : obstacleList) {
                    if (obstacles.getActionDown()) {
                        if (isInArena(coordinates)) {
                            Log.d(TAG, "C First: " + coordinates[0]);
                            Log.d(TAG, "C Second: " + coordinates[1]);
                            //Jon commented this out, not sure what it does
//                            isInCell(x,y);
                            obstacles.setObsMapCoord(coordinates[0], coordinates[1]);
                            obstacles.setaObsX(coordinates[0]);
                            Log.d(TAG, "Obstacle Coord x = " + obstacles.getaObsX());

                            if (coordinates[1] == -1) {
                                //When inverse, 0 = 19
                                obstacles.setaObsY(convertRow(0));
                            } else {
                                obstacles.setaObsY(coordinates[1] - 1);
                            }

                            Log.d(TAG, "Obstacle Coord y = " + obstacles.getaObsY());




                        } else {
                            // Out of bounds
                            obstacles.setObsX(obstacles.getInitCoords()[0]);
                            obstacles.setObsY(obstacles.getInitCoords()[1]);

//                          not sure what this does but seems like nothing
//                            int initX = obstacles.getObsMapCoord()[0];
//                            int initY = convertRow(obstacles.getObsMapCoord()[1] -1);
//
////                            obstacles.setPosition(obstacles.getInitCoords()[0], obstacles.getInitCoords()[1]);
//                            obstacles.setObsMapCoord(-1, -1);
//
//                            //Direct message to Main Activity
//                            if (initX != -1 && initY != -1){
////                                MainActivity.printMessage("SUBOBSTACLE," + obstacles.getObsID() + "," + initX  + "," + initY);
//                            }
                        }
                    }
                    obstacles.setActionDown(false);
                    obstacles.setResizeUp(false);
                    obstacles.setFaceResizeUp(false);
                    invalidate();
                }

                break;
        }

        Log.d(TAG, "onTouchEvent: Exiting onTouchEvent");
        //Must be true, else it will only call ACTION_DOWN
        return true;
        //return super.onTouchEvent(event);
    }

    //this function isnt used
    public String getObstacles(){
        String obsDetailsString = "";
        for (Obstacle obstacles : obstacleList) {

            if (!((obstacles.getaObsX() == 0) && (obstacles.getaObsY() == 0) && (obstacles.getObsFace().equals(" ")))){

                Log.d(TAG, "x = " + obstacles.getaObsX());
                Log.d(TAG, "y = " + obstacles.getaObsY());

                String ADD = "ADDOBSTACLE," + obstacles.getObsID() + "," + obstacles.getaObsX() + "," + obstacles.getaObsY() + ",";
                String FACE = "OBSTACLEFACE," + obstacles.getObsID() + "," + obstacles.getObsFace() + ",";
//                obsDetailsString = ADD.concat(FACE);
                obsDetailsString = obsDetailsString.concat(ADD.concat(FACE));


            }
        }
        Log.d(TAG, obsDetailsString);
        return obsDetailsString;
    }

    //Draw shapes on the canvas
    @Override
    protected  void onDraw(Canvas canvas){
        super.onDraw(canvas);

        //Set width and height of the canvas
        int width = getWidth();
        int height = getHeight();

        Log.d(TAG,"Width and Height: " + width + height);

        //jon commented out these
        //Calculate cellsize based on dimensions of the canvas
//        if(width/height < COLS/ROWS){
//            cellSize = width / (COLS + 1);
//            Log.d(TAG,"Cell size 1: " + cellSize);
//        } else {
//            cellSize = height / (ROWS + 1);
//            Log.d(TAG,"Cell size 2: " + cellSize);
//        }

        cellSize = height/(ROWS + 1);
        Log.d(TAG,"The Cell's size: " + cellSize);

        //Calculate margin size of canvas
        hMargin = ((width - COLS * cellSize) / 2 - 45);
        vMargin = (height - ROWS * cellSize) / 2;


        //Create cell
        if(!createCellStatus){
            //Create cell coordincates
            //Log.d(TAG, "onDraw: Creating cells");
            createCells();
            createCellStatus = true;
        }

        //Set Margin
        canvas.translate(hMargin, vMargin);

        drawBorder(canvas);
        drawCells(canvas);
        drawGridNumber(canvas);

        for(Obstacle obstacles : obstacleList) {
            obstacles.drawObj(canvas);
            obstacles.drawObsFace(canvas, obstacles.getTouchCount(), linePaint);

            canvas.drawText(obstacles.getTargetID(), obstacles.getObsX() + 9, obstacles.getObsY() + 21, obstacleNumberPaint);
//            paintObsFace(canvas);
        }

    }

    private void drawCells(Canvas canvas){
        for (int x = 0; x < COLS; x++) {
            for (int y = 0; y < ROWS; y++) {
                //Draw cells
                canvas.drawRect(cells[x][y].startX,cells[x][y].startY,cells[x][y].endX,cells[x][y].endY,cells[x][y].paint);
            }
        }
    }

    //Draw border for each cell
    private void drawBorder(Canvas canvas){
        for (int x = 0; x < COLS; x++) {
            for (int y = 0; y < ROWS; y++) {
                //Top
                canvas.drawLine(x * cellSize, y * cellSize, (x + 1) * cellSize, y * cellSize, wallPaint);
                //Right
                canvas.drawLine((x + 1) * cellSize, y * cellSize, (x + 1) * cellSize, (y + 1) * cellSize, wallPaint);
                //Left
                canvas.drawLine(x * cellSize, y * cellSize, x * cellSize, (y + 1) * cellSize, wallPaint);
                //Bottom
                canvas.drawLine(x * cellSize, (y + 1) * cellSize, (x + 1) * cellSize, (y + 1) * cellSize, wallPaint);
            }
        }
    }




    //Draw numbers
    private void drawGridNumber(Canvas canvas) {
        //Row
        for (int x = 0; x < 20; x++) {
            if(x >9 && x <20){
                canvas.drawText(Integer.toString(x), cells[x][19].startX + (cellSize / 5), cells[x][19].endY + (cellSize / 1.5f), gridNumberPaint);
            } else {
                canvas.drawText(Integer.toString(x), cells[x][19].startX + (cellSize / 3), cells[x][19].endY + (cellSize / 1.5f), gridNumberPaint);
            }
        }
        //Column
        for (int x = 0; x <20; x++) {
            if(x >9 && x <20){
                canvas.drawText(Integer.toString(19 - x), cells[0][x].startX - (cellSize / 1.5f), cells[0][x].endY - (cellSize / 3.5f), gridNumberPaint);
            } else {
                canvas.drawText(Integer.toString(19 - x), cells[0][x].startX - (cellSize / 1.2f), cells[0][x].endY - (cellSize / 3.5f), gridNumberPaint);
            }
        }
    }

    //Inverting rows
    private int convertRow(int y){
        return (19 - y);
    }

    //jon: so far not useful
    private void updateTargetText(String obsID, String targetID) {
        //Go through list of obstacles
        String ID;
        for (Obstacle obstacles : obstacleList) {
            ID = obstacles.getObsID();
            if(ID.equals(obsID)){
                Log.d(TAG,"obsID: " + obsID);
                Log.d(TAG,"targetID: " + targetID);
                obstacles.setTargetID(targetID);
            }
        }
        invalidate();
    }

    //Resetting Arena by resetting everything
    public void resetMap(){
        curCoord = new int [] {-1, -1};
        robotDirection = "north";
        createCellStatus = false;
        setRobotPostition = false;
        canDrawRobot = false;

        for (Obstacle obstacles : obstacleList){
            obstacles.setObsX(obstacles.getInitCoords()[0]);
            obstacles.setObsY(obstacles.getInitCoords()[1]);
            obstacles.setTargetID(obstacles.getObsID());
            obstacles.setaObsX(0);
            obstacles.setaObsY(0);

            obstacles.setTouchCount(0);
            obstacles.setLongPress(false);
        }

//        setStartingPoint(false);
//        MainActivity.setRobotDetails(-1, -1, "north");
        MainActivity.setXCoord(0);
        MainActivity.setyCoord(0);

        invalidate();
    }

    private ArrayList<int[]> getObstacleCoord() {
        return obstacleCoord;
    }

    private boolean isInArena(int touchedCoord []){
        //Check if coordinates is within the Arena
        Log.d(TAG,"isInArena: Check if touched coordinates is within the Arena");
        boolean isInArena = false;

//        if(touchedCoord[1] < -1){
//            return false;
//        }

        //If in Arena, return true
        if (touchedCoord[0] != -1 && touchedCoord[1] != -1) {
            isInArena = true;
        } else if (touchedCoord [0] != -1 && touchedCoord[1] == -1){
            isInArena = true;
        }

        return isInArena;
    }

    private int[] isInCell(int x, int y){
        //Check if coordinates is within the Cell, set to the nearest position
        Log.d(TAG,"isInCell: Check if obstacle coordinates is within the Cell");

        return new int [] {1,2};
    }



    public void getStartX(){

    }
    public void getStartY(){

    }
    public void getEndX(){

    }
    public void getEnd(){

    }
    //Find coordinates of cell in arena
    public static int[] findGridOnTouch(float x, float y) {
        int row = -1, cols = -1;
        for (int i = 0; i < COLS; i++) {
            //this if condition is checking if the touch coord is in the range of the cell
            if (cells[i][0].endX >= (x - hMargin) && cells[i][0].startX <= (x - hMargin)) {
                cols = i;
                Log.d(TAG, "SDATA startX = " + cells[i][0].startX);
                Log.d(TAG, "SDATA endX = " + cells[i][0].endX);
                Log.d(TAG, "SDATA cols = " + cols);
                Log.d(TAG, "hMargin = " + hMargin);
                Log.d(TAG, "x = " + x);
                Log.d(TAG, "hMargin = " + (x - hMargin));
                break;
            }
        }
        for (int j = 0; j < ROWS; j++) {
            //this if condition is checking if the touch coord is in the range of the cell
            if (cells[0][j].endY >= (y - vMargin) && cells[0][j].startY <= (y - vMargin)) {
                row = j;
                Log.d(TAG, "SDATA startY = " + cells[0][j].startY);
                Log.d(TAG, "SDATA endY = " + cells[0][j].endY);
                Log.d(TAG, "SDATA row = " + row);
                Log.d(TAG, "hMargin = " + vMargin);
                Log.d(TAG, "y = " + y);
                Log.d(TAG, "hMargin = " + (y - vMargin));
                break;
            }
        }
        return new int[]{cols, row};
    }


    private void setValidPosition(boolean status) {
        validPosition = status;
    }

    private boolean getValidPosition() {
        return validPosition;
    }


    private class Cell {
        float startX, startY, endX, endY;
        Paint paint;
        String type;

        private Cell(float startX, float startY, float endX, float endY, Paint paint){
            this.startX = startX;
            this.startY = startY;
            this.endX = endX;
            this.endY = endY;
            this.paint = paint;
        }

        public void setPaint(Paint paint){
            this.paint = paint;
        }

        public void setType(String type) {
            this.type = type;
            switch (type) {
                case "obstacle":
                    this.paint = obstaclePaint;
                    break;
                case "robot":
                    this.paint = robotPaint;
                    break;
                case "unexplored":
                    this.paint = unexploredPaint;
                    break;
                case "explored":
                    this.paint = exploredPaint;
                    break;
                case "arrow":
                    this.paint = directionPaint;
                    break;
                case "id":
                    this.paint = obstacleNumberPaint;
                    break;
                default:
                    Log.d(TAG,"setTtype default: " + type);
                    break;
            }
        }
    }

    public class LongPressGestureListener extends GestureDetector.SimpleOnGestureListener {

        public LongPressGestureListener(View arenaMap) {
        }

        @Override
        public void onLongPress(MotionEvent e) {
            super.onLongPress(e);
            Log.d("TAG","onLongPress: LONG PRESS!");

            int x = (int) e.getX();
            int y = (int) e.getY();

            //Increase counts for annotation
            for (Obstacle obstacles : obstacleList) {
                //If the obstacle is longPressed, sets status to true and toasts face annotation enabled
                //otherwise toasts that its disabled
                if (obstacles.isTouched(x, y)) {
                    obstacles.setActionDown(false);
                    if(obstacles.getLongPress()){
                        Toast.makeText(getContext(), "Face annotation disabled", Toast.LENGTH_LONG).show();
                        obstacles.setLongPress(false);
                    } else {
                        Toast.makeText(getContext(), "Face annotation enabled", Toast.LENGTH_LONG).show();
                        obstacles.setLongPress(true);
                    }
                }
            }
        }

        @Override
        public boolean onDown(MotionEvent e) {
            return true;
        }
    }



}