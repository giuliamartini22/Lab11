from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.go_products import go_product


class DAO():

    @staticmethod
    def getAllYears() -> list[tuple[int]] | None:
        cnx = DBConnect.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = """SELECT DISTINCT YEAR(gds.Date)
                        FROM go_daily_sales gds"""
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
            return rows
        else:
            print("Errore nella connessione")
            return None

    @staticmethod
    def getAllColors() -> list[tuple[str]]:
        cnx = DBConnect.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = """select distinct gp.Product_color 
                    from go_products gp """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            cnx.close()
            return rows
        else:
            print("Errore di connessione")
            return None

    @staticmethod
    def getAllFilteredProducts(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_products gp 
                    where gp.Product_color = %s"""

        cursor.execute(query, (color,))

        for row in cursor:
            result.append(go_product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno, color, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #manca il distinct di GS1.Date

        #query = """select gds1.Product_number as PN1, gds2.Product_number as PN2, DISTINCT(gds1.Date) as Date
        #            from go_daily_sales gds1, go_daily_sales gds2, go_products gp, go_products gp2
        #            where gds1.Retailer_code = gds2.Retailer_code
        #            and gds1.`Date`  = gds2.`Date`
        #            and gds1.Product_number < gds2.Product_number
        #            and year(gds1.`Date`) = %s
        #            and gp.Product_number = gds1.Product_number
        #            and gp2.Product_number = gds2.Product_number
        #            and gp.Product_color = %s
        #            and gp2.Product_color = %s
        #            """

        query = """select distinct gds2.`Date`, gds1.Product_number as PN1, gds2.Product_number as PN2
                    from go_daily_sales gds1, go_daily_sales gds2, go_products gp, go_products gp2 
                    where gds1.Retailer_code = gds2.Retailer_code
                    and gds1.`Date`  = gds2.`Date` 
                    and gds1.Product_number < gds2.Product_number 
                    and year(gds1.`Date`) = %s
                    and gp.Product_number = gds1.Product_number
                    and gp2.Product_number = gds2.Product_number
                    and gp.Product_color = %s
                    and gp2.Product_color = %s
        """

        cursor.execute(query, (anno,color,color,))

        for row in cursor:
            result.append(Connessione(idMap[row["PN1"]],
                                      idMap[row["PN2"]]
                                      ))

        cursor.close()
        conn.close()
        return result