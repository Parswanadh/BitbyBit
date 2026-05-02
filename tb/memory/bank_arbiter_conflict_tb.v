module bank_arbiter_conflict_tb();
    reg clk, rst_n;
    reg [127:0] req;
    wire [127:0] gnt;

    bank_arbiter uut (.clk(clk), .rst_n(rst_n), .req(req), .gnt(gnt));

    initial begin
        clk = 0; rst_n = 0; req = 128'hFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
        #10 rst_n = 1;
        #100 $finish;
    end
    always #5 clk = ~clk;
endmodule
