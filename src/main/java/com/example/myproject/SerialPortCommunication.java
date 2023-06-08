package com.example.myproject;
import com.fazecast.jSerialComm.*;
import java.util.Arrays;

public class SerialPortCommunication {
    private static final String SERIAL_PORT_NAME = "/dev/ttyUSB0";
    private static final int BAUD_RATE = 9600;

    public void sendAndReceiveData() {
        // Open the serial port
        SerialPort serialPort = SerialPort.getCommPort(SERIAL_PORT_NAME);
        serialPort.setBaudRate(BAUD_RATE);

        if (serialPort.openPort()) {
            System.out.println("Serial port opened successfully.");

            // Read data from the serial port
            byte[] receivedData = new byte[1024];
            int numBytes = serialPort.readBytes(receivedData, receivedData.length);
            receivedData = Arrays.copyOf(receivedData, numBytes);
            String receivedDataString = new String(receivedData);
            System.out.println("Received data: " + receivedDataString);

            // Close the serial port
            serialPort.closePort();
            System.out.println("Serial port closed.");
        } else {
            System.err.println("Failed to open the serial port.");
        }
    }

    public static void main(String[] args) {
        SerialPortCommunication serialCommunication = new SerialPortCommunication();
        serialCommunication.sendAndReceiveData();
    }
}