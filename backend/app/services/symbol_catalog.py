def get_symbol_catalog():
    forex_pairs = [
        "frxEURUSD",
        "frxGBPUSD",
        "frxUSDJPY",
        "frxAUDUSD",
        "frxUSDCAD",
        "frxNZDUSD",
        "frxEURJPY",
        "frxGBPJPY",
        "frxEURCHF",
        "frxAUDJPY",
        "frxUSDCHF",
        "frxEURGBP",
        "frxGBPCHF",
        "frxEURAUD",
    ]

    synthetics = [
        "R_50",
        "R_100",
        "R_200",
        "1HZ10V",
        "1HZ50V",
        "1HZ100V",
        "B_10",
        "B_25",
        "B_50",
        "B_75",
        "B_100",
    ]

    return forex_pairs + synthetics
