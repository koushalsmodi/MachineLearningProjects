# 🛒 Smart Shopper Agent

An Agentic AI prototype that autonomously searches, recommends, and purchases products from the Mini-Shop API - enforcing user budgets and logging all actions.

## ✨ Features
- 💬 Natural-language goal input
- 🔧 Dynamic tool calling (recommend → add_to_cart → checkout)
- 💰 Hardcoded budget guardrail ($500)
- 📋 Full audit logging to `logs/mini_shop.log`

## 🛠️ Tech Stack
- **FastAPI** backend (`main.py`)
- **LangChain + Anthropic Claude** for reasoning
- **Python logging** for audit trail
- **Memory store** for preferences

## 🚀 Quick Start
```bash
fastapi dev main.py          # start API
python3 agent_runner.py      # run agent
```

## 📊 Architecture
The agent operates autonomously within defined constraints, making intelligent purchasing decisions while maintaining full transparency through comprehensive logging.

## 📸 Example Output

**Successful autonomous purchase flow:**

```bash
=== Starting Agent ===

Iteration 1
Calling tool: recommend with args: {'user_query': 'best product under $500 budget'}
Tool result: Based on your $500 budget, I recommend:

**HP Spectre - $249**
- Great laptop option well within your budget
- Leaves you with $251 to spare
- In stock with 40 units available

Iteration 2
Calling tool: add_to_cart with args: {'product_id': 2, 'quantity': 1}
Tool result: Added product ID: 2 (quantity: 1) to the cart.

Iteration 3
Calling tool: checkout with args: {}
Tool result: Purchase confirmed. Order placed successfully.

=== Final Response ===
✅ **Order Complete!**

I've successfully recommended and purchased the **HP Spectre laptop for $249** - 
a great mid-range laptop that fits well within your $500 budget. 
Your order has been placed and confirmed.

You saved $251 from your budget while getting an excellent quality laptop.
```

**Key Capabilities Demonstrated:**
- 🎯 Autonomous decision-making across 3 tool calls
- 💵 Budget compliance verified ($249 < $500)
- 📝 Complete audit trail in logs
- ✅ End-to-end transaction completion
