package com.example.myproject;
import org.yamcs.tse.SerialPortDriver;

public class SerialPortDriver {
    public static void main(String[] args) {
        SerialPortDriver driver = new SerialPortDriver();

        driver.setBaudrate(9600);
        driver.setDataBits(8);
        driver.setParity("None");
        driver.setPath("/dev/ttyUSB0");

        driver.connect();

        byte[] data ={0x001, 0x02, 0x03};
        driver.write(data);

        byte[] buffer = new byte[1024];
        int bytesRead = driver.read(buffer);

        driver.disconnect();
    }
}
