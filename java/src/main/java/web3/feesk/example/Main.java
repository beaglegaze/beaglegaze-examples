package web3.beaglegaze.example;

import web3.beaglegaze.PayPerCall;

public class Main {

    @PayPerCall(price = 100L)
    public static void main(String[] args) throws Exception {
        System.out.println("Successfully called main method!");
    }
}