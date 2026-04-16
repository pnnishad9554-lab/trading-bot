import argparse
import logging
from client import place_market_order, place_limit_order

# Setup logging
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    try:
        logging.info(f"Order Request: {vars(args)}")

        print("\n📤 Order Request:")
        print(vars(args))

        if args.type == "MARKET":
            response = place_market_order(
                args.symbol,
                args.side,
                args.quantity
            )

        elif args.type == "LIMIT":
            if args.price is None:
                raise ValueError("Price is required for LIMIT orders")

            response = place_limit_order(
                args.symbol,
                args.side,
                args.quantity,
                args.price
            )

        logging.info(f"API Response: {response}")

        print("\n📦 API Response:")
        print(response)

        print("\n✅ Order Summary:")
        print(f"Order ID: {response.get('orderId', 'N/A')}")
        print(f"Status: {response.get('status', 'N/A')}")
        print(f"Executed Quantity: {response.get('executedQty', 'N/A')}")
        print(f"Average Price: {response.get('avgPrice', 'N/A')}")

        print("\n🎉 Order executed successfully!")

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        print("\n❌ Error:")
        print(str(e))


if __name__ == "__main__":
    main()