def timer_output(time, field, emit_frequency=5, num_bikes=3808):
        """
        Format output text
        """
        if field == "emit":
            if time <= emit_frequency:
                return f"\033[94m{num_bikes} calls finished in \033[92m{time:.4f}\033[94m seconds"
            if time > emit_frequency:
                return f"\033[94m{num_bikes} calls finished in \033[91m{time:.4f}\033[94m seconds"
            return f"\033[94m{num_bikes} calls finished in \033[93m{time:.4f}\033[94m seconds"
        if field == "route":
            return f"\033[94mGenerated {num_bikes} routes in in \033[92m{time:.4f}\033[94m seconds"
        if field == "activation":
            return f"\033[94mIterated through {num_bikes} bikes with activation \033[92m{time:.4f}\033[94m seconds"
        if field == "active":
            return f"\033[94mIterated through {num_bikes} active bikes \033[92m{time:.4f}\033[94m seconds"
        if field == "total":
            return f"\033[94mTotal loop time was \033[92m{time:.4f}\033[94m seconds"