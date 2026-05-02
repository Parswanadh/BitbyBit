`timescale 1ns/1ps

module bank_arbiter_tb;

    parameter NUM_UNITS = 16;
    parameter NUM_BANKS = 8;

    reg clk;
    reg rst_n;
    reg [NUM_UNITS-1:0] req [0:NUM_BANKS-1];
    wire [NUM_UNITS-1:0] gnt [0:NUM_BANKS-1];

    bank_arbiter #(
        .NUM_UNITS(NUM_UNITS),
        .NUM_BANKS(NUM_BANKS)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .req(req),
        .gnt(gnt)
    );

    always #5 clk = ~clk;

    integer b, u;

    initial begin
        $dumpfile("bank_arbiter_tb.vcd");
        $dumpvars(0, bank_arbiter_tb);

        clk = 0;
        rst_n = 0;
        for (b = 0; b < NUM_BANKS; b = b + 1) req[b] = 0;

        #20 rst_n = 1;

        // Issue simultaneous requests from all units to bank 0
        #10;
        for (u = 0; u < NUM_UNITS; u = u + 1) begin
            req[0][u] = 1;
        end

        // Observe grants over several cycles
        #100;
        
        // Disable all requests
        for (u = 0; u < NUM_UNITS; u = u + 1) begin
            req[0][u] = 0;
        end

        #20;
        $finish;
    end

    // Monitor for verification
    always @(posedge clk) begin
        if (rst_n) begin
            integer granted_count;
            granted_count = 0;
            for (u = 0; u < NUM_UNITS; u = u + 1) begin
                if (gnt[0][u]) granted_count = granted_count + 1;
            end
            
            if (granted_count > 1) begin
                $display("FAIL: Multiple grants detected at time %t!", $time);
                $finish;
            end
        end
    end

endmodule
