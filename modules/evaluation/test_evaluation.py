class ContextEvaluator:


    def length_score(
        self,
        context
    ):


        words=len(
            context.split()
        )


        if words < 100:

            return 0


        if words < 500:

            return 1


        return 2