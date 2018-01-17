from datetime import date

_dict = {
        'have_position': False, # Boolean if have position
        'reached_target': False, # Boolean have made daily net profit
        'profit_loss': float(0.00), # Float daily nominal PL with trading costs
        

    }

_dict[str(date.today())] = date.today()

print(_dict)